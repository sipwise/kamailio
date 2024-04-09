#!/usr/bin/perl

#
# Generate select lists from ser/sip-router select initializations structs.
# (run on files generated by gcc -fdump-translation-unit -c file.c, 
#  try -h for help)
# E.g.: dump_selects.pl --file cfg_core.c  --defs="-DUSE_SCTP ..."
#

# Note: uses GCC::TranslationUnit (see cpan) with the following patch:
#@@ -251,6 +251,8 @@
# 	    $node->{vector}[$key] = $value;
# 	} elsif($key =~ /^op (\d+)$/) {
# 	    $node->{operand}[$1] = $value;
#+	} elsif ($key eq "val") {
#+		push @{$node->{$key}}, ($value) ;
# 	} else {
# 	    $node->{$key} = $value;
# 	}
# 
#
# Assumptions:
#  - the first array of type select_row_t  with an initializer is the array
#    with the select definitions. Only one select_row_t array per file is
#    supported.
#
# Output notes:
#

use strict;
use warnings;
use Getopt::Long;
use File::Temp qw(:mktemp);
use File::Basename;
use GCC::TranslationUnit;

# text printed if we discover that GCC::TranslationUnit is unpatched
my $patch_required="$0 requires a patched GCC:TranslationUnit, see the " .
				"comments at the beginning of the file or try --patch\n";
# gcc name
my $gcc="gcc";
# default defines
my $c_defs="DNAME='\"kamailio\"' -DVERSION='\"5.1.0-dev3\"' -DARCH='\"x86_64\"' -DOS='linux_' -DOS_QUOTED='\"linux\"' -DCOMPILER='\"gcc 4.9.2\"' -D__CPU_x86_64 -D__OS_linux -DSER_VER=5001000 -DCFG_DIR='\"/usr/local/etc/kamailio/\"' -DRUN_DIR='\"/run/kamailio/\"' -DPKG_MALLOC -DSHM_MEM -DSHM_MMAP -DDNS_IP_HACK -DUSE_MCAST -DUSE_TCP -DDISABLE_NAGLE -DHAVE_RESOLV_RES -DUSE_DNS_CACHE -DUSE_DNS_FAILOVER -DUSE_DST_BLOCKLIST -DUSE_NAPT -DMEM_JOIN_FREE -DF_MALLOC -DQ_MALLOC -DTLSF_MALLOC -DDBG_SR_MEMORY -DUSE_TLS -DTLS_HOOKS -DUSE_CORE_STATS -DSTATISTICS -DMALLOC_STATS -DWITH_AS_SUPPORT -DUSE_SCTP -DFAST_LOCK -DADAPTIVE_WAIT -DADAPTIVE_WAIT_LOOPS=1024 -DCC_GCC_LIKE_ASM -DHAVE_GETHOSTBYNAME2 -DHAVE_UNION_SEMUN -DHAVE_SCHED_YIELD -DHAVE_MSG_NOSIGNAL -DHAVE_MSGHDR_MSG_CONTROL -DHAVE_ALLOCA_H -DHAVE_TIMEGM -DHAVE_SCHED_SETSCHEDULER -DHAVE_IP_MREQN -DHAVE_EPOLL -DHAVE_SIGIO_RT -DSIGINFO64_WORKAROUND -DUSE_FUTEX -DHAVE_SELECT";

# file with gcc syntax tree
my $file;
my $core_file;
my $src_fname;

# type to look for
my $var_type="select_row_t";

my $tu;
my $node;
my $i;
my @sel_exports; # filled with select definitions (select_row_t)
my @core_exports; # filled with select definitions from core (if -c is used)
my ($sel_grp_name, $sel_var_name);

my ($opt_help, $opt_txt, $opt_is_tu, $dbg, $opt_grp_name, $opt_patch);
my ($opt_force_grp_name, $opt_docbook);

# default output formats
my $output_format_header="HEADER";
my $output_format_footer="FOOTER";
my $output_format_selline="SELLINE";


sub show_patch
{
my $patch='
--- GCC/TranslationUnit.pm.orig	2009-10-16 17:57:51.275963053 +0200
+++ GCC/TranslationUnit.pm	2009-10-16 20:17:28.128455959 +0200
@@ -251,6 +251,8 @@
 	    $node->{vector}[$key] = $value;
 	} elsif($key =~ /^op (\d+)$/) {
 	    $node->{operand}[$1] = $value;
+	} elsif ($key eq "val") {
+		push @{$node->{$key}}, ($value) ;
 	} else {
 	    $node->{$key} = $value;
 	}
';

print $patch;
}


sub help
{
	$~ = "USAGE";
	write;

format USAGE =
Usage @*  -f filename | --file filename  [options...]
      $0
Options:
         -f        filename    - use filename for input (see also -T/--tu).
         --file    filename    - same as -f.
         -c | --core filename  - location of core selects (used to resolve
                                 module selects that refer in-core functions).
         -h | -? | --help      - this help message.
         -D | --dbg | --debug  - enable debugging messages.
         -d | --defs           - defines to be passed on gcc's command line
                                 (e.g. --defs="-DUSE_SCTP -DUSE_TCP").
         -g | --grp  name
         --group     name      - select group name used if one cannot be
                                 autodetected (e.g. no default value 
                                 initializer present in the file).
         -G | --force-grp name
         --force-group    name - force using a select group name, even if one
                                 is autodetected (see also -g).
         --gcc     gcc_name    - run gcc_name instead of gcc.
         -t | --txt            - text mode output.
         --docbook | --xml     - docbook output (xml).
         -T | --tu             - the input file is in raw gcc translation
                                 unit format (as produced by
                                   gcc -fdump-translation-unit -c ). If not
                                 present it's assumed that the file contains
                                 C code.
         -s | --src | --source - name of the source file, needed only if
                                 the input file is in "raw" translation
                                 unit format (--tu) and useful to restrict
                                 and speed-up the search.
         --patch               - show patches needed for the
                                 GCC::TranslationUnit package.
.

}



# escape a string for xml use
# params: string to be escaped
# return: escaped string
sub xml_escape{
	my $s=shift;
	my %escapes = (
		'"' => '&quot;',
		"'" => '&apos;',
		'&' => '&amp;',
		'<' => '&lt;',
		'>' => '&gt;'
	);
	
	$s=~s/(["'&<>])/$escapes{$1}/g;
	return $s;
}



# escape a string according with the output requirements
# params: string to be escaped
# return: escaped string
sub output_esc{
	return xml_escape(shift) if defined $opt_docbook;
	return shift;
}



# eliminate casts and expressions.
# (always go on the first operand)
# params: node (GCC::Node)
# result: if node is an expression it will walk on operand(0) until first non
# expression element is found
sub expr_op0{
	my $n=shift;
	
	while(($n->isa('GCC::Node::Expression') || $n->isa('GCC::Node::Unary')) &&
			defined $n->operand(0)) {
		$n=$n->operand(0);
	}
	return $n;
}


# constants (from select.h)
use constant {
	MAX_SELECT_PARAMS =>	32,
	MAX_NESTED_CALLS =>		4,
};

use constant DIVERSION_MASK => 0x00FF;
use constant {
	DIVERSION =>			1<<8,
	SEL_PARAM_EXPECTED =>	1<<9,
	CONSUME_NEXT_STR =>		1<<10,
	CONSUME_NEXT_INT =>		1<<11,
	CONSUME_ALL =>			1<<12,
	OPTIONAL =>				1<<13,
	NESTED =>				1<<14,
	FIXUP_CALL =>			1<<15,
};

use constant {
	SEL_PARAM_INT => 0,
	SEL_PARAM_STR => 1,
	SEL_PARAM_DIV => 2,
	SEL_PARAM_PTR => 3,
};



# Select rules (pasted from one email from Jan):
# Roughly the rules are as follows:
# * The first component of the row tells the select compiler in what state the
#   row can be considered.
# * The second component tells the compiler what type of components is expected
#   for the row to match. SEL_PARAM_STR means that .foo should follow,
#   SEL_PARAM_INT means that [1234] should follow.
# * The third component is the string to be matched for string components and
#   STR_NULL if the next expected component is an integer.
# * The fourth component is a function name. This is either the function to be
#   called if this is the last rule all constrains are met, or it is the next
#   state to transition into if we are not processing the last component of the
#   select identifier.
#
# * The fifth rule are flags that can impose further constrains on how the
#   given line is to be used. Some of them are:
#
# - CONSUME_NEXT_INT - This tells the compiler that there must be at least one 
#   more component following the current one, but it won't transition into the
#   next state, instead the current function will "consume" the integer as
#   parameters.
#
# - CONSUME_NEXT_STR - Same as previous, but the next component must be a
#   string.
# - SEL_PARAM_EXPECTED - The current row must not be last and there must be
#   another row to transition to.
#
# - OPTIONAL - There may or may not be another component, but in any case the
#   compiler does not transition into another state (row). This can be used
#   together with CONSUME_NEXT_{STR,INT} to implement optional parameters, for
#   example .param could return a string of all parameters, while .param.abc
#   will only return the value of parameter abc.
# 
# - NESTED - When this flag is present in a rule then it means that the
#   previous function should be called before the current one. The original
#   idea was that all select identifiers would only resolve to one function
#   call, however, it turned out to be inconvenient in some cases so we added
#   this. This is typically used in selects that have URIs as components. In
#   that case it is desirable to support all subcomponents for uri selects, but
#   it does not make sense to reimplement them for every single case. In that
#   case the uri components sets NESTED flags which causes the "parent"
#   function to be called first. The "parent" function extracts only the URI
#   which is then passed to the corresponding URI parsing function. The word
#   NESTED here means "nested function call".
#
# - CONSUME_ALL - Any number of select identifier components may follow and
#   they may be of any types. This flag causes the function on the current row
#   to be called and it is up to the function to handle the remainder of the
#   select identifier.



# generate all select strings starting with a specific "root" function
# params:
#  $1 - root
#  $2 - crt_label/skip (if !="" skip print and use it to search the next valid
#       sel. param)
sub gen_selects
{
	my $root=shift;
	my $crt_label=shift;
	my $skip_next;
	my @matches;
	my ($prev, $type, $name, $new_f, $flags);
	my $m;
	my @ret=();
	my @sel;
	
	@matches = grep((${$_}[0] eq $root) &&
					(!defined $crt_label || $crt_label eq "" ||
					 ${$_}[2] eq "" ||
					 $crt_label eq ${$_}[2]) , @sel_exports);
	if ((@matches == 0) && (@core_exports > 0)) {
		@matches = grep((${$_}[0] eq $root) &&
					(!defined $crt_label || $crt_label eq "" ||
					 ${$_}[2] eq "" ||
					 $crt_label eq ${$_}[2]), @core_exports);
	}
	for $m (@matches) {
		my $s="";
		($prev, $type, $name, $new_f, $flags)=@$m;
		if (($flags & (NESTED|CONSUME_NEXT_STR|CONSUME_NEXT_INT)) == NESTED){
			$skip_next=$name;
		}
		if (!($flags & NESTED) ||
			(($flags & NESTED) && ($type !=SEL_PARAM_INT))){
			# Note: unnamed NESTED params are not allowed --andrei
			if ($type==SEL_PARAM_INT){
				$s.="[integer]";
			}else{
				if ($name ne "") {
					if (!defined $crt_label || $crt_label eq "") {
						$s.=(($prev eq "0" || $prev eq "")?"@":".") . $name;
					}
				}elsif (!($flags & NESTED) &&
						(!defined $crt_label || $crt_label eq "")){
					$s.=".<string>";
				}
			}
		}
		if ( !($flags & NESTED) &&
			 ($flags & (CONSUME_NEXT_STR|CONSUME_NEXT_INT|CONSUME_ALL)) ){
			#process params
			if ($flags & OPTIONAL){
				$s.="{";
			}
			# add param name
			if ($flags & CONSUME_NEXT_STR){
				$s.="[\"string\"]";
			}elsif ($flags & CONSUME_NEXT_INT){
				$s.="[integer]";
			}else{
				$s.=".*"; # CONSUME_ALL
			}
			if ($flags & OPTIONAL){
				$s.="}";
			}
		}
		
		if (!($flags & SEL_PARAM_EXPECTED)){
			# if optional terminal  add it to the list along with all the
			# variants
			if ($new_f eq "" || $new_f eq "0"){
				# terminal
				push @ret, $s;
			}else{
				@sel=map("$s$_", gen_selects($new_f, $skip_next));
				if (@sel > 0) {
					push(@ret, $s) if (!($s eq "") && !($flags & NESTED));
					push @ret, @sel;
				}else{
					if ($flags & NESTED) {
						$s.="*";
					}
					push @ret, $s;
				}
			}
		}else{
			# non-terminal
			if (!($new_f eq "" || $new_f eq "0")){
				@sel=map("$s$_", gen_selects($new_f, $skip_next));
				if (@sel > 0) {
					push @ret, @sel;
				}elsif ($flags & NESTED){
					$s.="*";
					push @ret, $s;
				}
			} # else nothing left, but param expected => error
		}
	}
	return @ret;
}



# parse the select declaration from a  file into an array.
# params:
#  $1 - file name
#  $2 - ref to result list (e.g. \@res)
#  $3 - boolean - true if filename is a translation-unit dump.
# cmd. line global options used:
#  $src_fname - used only if $3 is true (see --src)
#  $gcc
#  $c_defs
#  $dbg
#  
#
sub process_file
{
	my $file=shift;
	my $sel=shift; # ref to result array
	my $file_is_tu=shift;
	
	my $tmp_file;
	my $i;
	my $node;
	my $tu;
	my @res; # temporary hold the result here
	
	if (! $file_is_tu){
		# file is not a gcc translation-unit dump
		# => we have to create one
		$src_fname=basename($file);
		$tmp_file = "/tmp/" . mktemp ("dump_translation_unit_XXXXXX");
		# Note: gcc < 4.5 will produce the translation unit dump in a file in
		# the current directory. gcc 4.5 will write it in the same directory as
		# the output file.
		system("$gcc -fdump-translation-unit $c_defs -c $file -o $tmp_file") == 0
			or die "$gcc -fdump-translation-unit $c_defs -c $file -o $tmp_file" .
				"  failed to generate a translation unit dump from $file";
		if (system("if [ -f \"$src_fname\".001t.tu ]; then \
						mv \"$src_fname\".001t.tu  $tmp_file; \
					else mv /tmp/\"$src_fname\".001t.tu  $tmp_file; fi ") != 0) {
			unlink($tmp_file, "$tmp_file.o");
			die "could not find the gcc translation unit dump file" .
					" ($src_fname.001t.tu) neither in the current directory" .
					" or /tmp";
		};
		$tu=GCC::TranslationUnit::Parser->parsefile($tmp_file);
		print(STDERR "src name $src_fname\n") if $dbg;
		unlink($tmp_file, "$tmp_file.o");
	}else{
		$tu=GCC::TranslationUnit::Parser->parsefile($file);
	}

	print(STDERR "Parsing file $file...\n") if $dbg;
	print(STDERR "Searching...\n") if $dbg;

	$i=0;
	# iterate on the entire nodes array (returned by gcc), but skipping node 0
	SEARCH: for $node (@{$tu}[1..$#{$tu}]) {
		$i++;
		while($node) {
			if (
				@res == 0 &&  # parse it only once
				$node->isa('GCC::Node::var_decl') &&
				$node->type->isa('GCC::Node::array_type') # &&
				#(! defined $src_fname || $src_fname eq "" ||
				#	$node->source=~"$src_fname")
				){
				# found a var decl. that it's an array
				# check if it's a valid array type
				next if (!(	$node->type->can('elements') &&
							defined $node->type->elements &&
							$node->type->elements->can('name') &&
							defined $node->type->elements->name &&
							$node->type->elements->name->can('name') &&
							defined $node->type->elements->name->name)
						);
				my $type_name= $node->type->elements->name->name->identifier;
				if ($type_name eq $var_type) {
					if ($node->can('initial') && defined $node->initial) {
						my %c1=%{$node->initial};
						$sel_var_name=$node->name->identifier;
						if (defined $c1{val}){
							my $c1_el;
							die $patch_required if (ref($c1{val}) ne "ARRAY");
							# iterate on array elem., level 1( top {} )
							# each element is a constructor.
							for $c1_el (@{$c1{val}}) {
								# finally we are a the lower {} initializer:
								#    { prev_f, type, name, new_f, flags }
								my %c2=%{$c1_el};
								my @el=@{$c2{val}};
								my ($prev_f_n, $type_n, $name_n, $new_f_n,
									$flags_n)=@el;
								my ($prev_f, $type, $name, $new_f, $flags);
								my $str;
								if ($prev_f_n->isa('GCC::Node::integer_cst') &&
									$new_f_n->isa('GCC::Node::integer_cst') &&
									$prev_f_n->low==0 && $new_f_n->low==0) {
									last SEARCH;
								}
								$prev_f=
									($prev_f_n->isa('GCC::Node::integer_cst'))?
										$prev_f_n->low:
										expr_op0($prev_f_n)->name->identifier;
								$type=$type_n->low;
								$str=${${$name_n}{val}}[0];
								$name=($str->isa('GCC::Node::integer_cst'))?"":
										expr_op0($str)->string;
								$new_f=
									($new_f_n->isa('GCC::Node::integer_cst'))?
										$new_f_n->low:
										expr_op0($new_f_n)->name->identifier;
								$flags= (defined $flags_n)?$flags_n->low:0;
								
								push @res, [$prev_f, $type, $name,
													$new_f, $flags];
							}
						}
					}
				}
			}
		} continue {
			if ($node->can('chain')){
				$node = $node->chain;
			}else{
				last;
			}
		}
	}
	push @$sel, @res;
}



# main:

# read command line args
if ($#ARGV < 0 || ! GetOptions(	'help|h|?' => \$opt_help,
								'file|f=s' => \$file,
								'core|c=s' => \$core_file,
								'txt|t' => \$opt_txt,
								'docbook|xml' => \$opt_docbook,
								'tu|T' => \$opt_is_tu,
								'source|src|s=s' => \$src_fname,
								'defs|d=s'=>\$c_defs,
								'group|grp|g=s'=>\$opt_grp_name,
								'force-group|force-grp|G=s' =>
													\$opt_force_grp_name,
								'dbg|debug|D'=>\$dbg,
								'gcc=s' => \$gcc,
								'patch' => \$opt_patch) ||
		defined $opt_help) {
	do { show_patch(); exit 0; } if (defined $opt_patch);
	select(STDERR) if ! defined $opt_help;
	help();
	exit((defined $opt_help)?0:1);
}

do { show_patch(); exit 0; } if (defined $opt_patch);
do { select(STDERR); help(); exit 1 } if (!defined $file);

if (defined $opt_txt){
	$output_format_header="HEADER";
	$output_format_footer="FOOTER";
	$output_format_selline="SELLINE";
}elsif (defined $opt_docbook){
	$output_format_header="DOCBOOK_HEADER";
	$output_format_footer="DOCBOOK_FOOTER";
	$output_format_selline="DOCBOOK_SELLINE";
}

process_file($file, \@sel_exports, defined $opt_is_tu);
process_file($core_file, \@core_exports, 0) if (defined $core_file);
print(STDERR "Done.\n") if $dbg;

my ($prev, $type, $name, $next, $flags, $desc);
my $extra_txt;

if (@sel_exports > 0){
	my $s;
	$i=0;
	# dump the configuration in txt mode
	if (defined $opt_force_grp_name) {
		$sel_grp_name=output_esc($opt_force_grp_name);
	}elsif (!defined $sel_grp_name && defined $opt_grp_name) {
		$sel_grp_name=output_esc($opt_grp_name);
	}
	print(STDERR "Generating select list...\n") if $dbg;
	my @sels = gen_selects "0";
	$~ = $output_format_header; write;
	$~ = $output_format_selline ;
	for $s (@sels){
		$extra_txt=output_esc("");
		$desc=output_esc("");
		$name=output_esc($s);
		$i++;
		#$extra_txt.=output_esc("Returns an array.") if ($flags & 1 );
		# generate txt description
		write;
	}
	$~ = $output_format_footer; write;
}else{
	die "no selects found in $file\n";
}


sub valid_grp_name
{
	my $name=shift;
	return defined $name && $name ne "";
}


format HEADER =
Selects@*
(valid_grp_name $sel_grp_name) ? " for " . $sel_grp_name : ""
=======@*
"=" x length((valid_grp_name $sel_grp_name)?" for " . $sel_grp_name : "")

@||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
"[ this file is autogenerated, do not edit ]"


.

format FOOTER =
.

format SELLINE =
@>>. @*
$i,  $name
~~      ^<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        $desc
~~      ^<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        $extra_txt
.


format DOCBOOK_HEADER =
<?xml version="1.0" encoding="UTF-8"?>
<!-- this file is autogenerated, do not edit! -->
<!DOCTYPE section PUBLIC "-//OASIS//DTD DocBook XML V4.2//EN"
	"http://www.oasis-open.org/docbook/xml/4.2/docbookx.dtd">
<chapter id="select_list@*">
(valid_grp_name $sel_grp_name) ? "." . $sel_grp_name : ""
	<title>Selects@*</title>
(valid_grp_name $sel_grp_name) ? " for " . $sel_grp_name : ""
	<orderedlist>


.

format DOCBOOK_FOOTER =
	</orderedlist>
</chapter>
.

format DOCBOOK_SELLINE =
	<listitem><simpara>@*</simpara>
					$name
~~<para>^<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< </para>
        $desc
~~<para>^<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< </para>
        $extra_txt
	</listitem>

.
