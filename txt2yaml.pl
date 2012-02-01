#!/usr/bin/perl

use Getopt::Long;
use constant{
	HELP => "this is a little help\n"
};


my ($in,$out,$help);

GetOptions('infile=s'=>\$in,'outfile'=>\$out,'help'=>\$help);

if ($help){
	&help;
	exit 0;
}


open IN, "<$in" or die "can't open file $!";


my %prefix=();
my %configs = ();
my ($regex,$pre,$type,$start); 
foreach my $line (<IN>){
	unless ($line =~ /^\s*$/){
		$line = lc($line);
		$line =~ s/\s+/ /g;
		local($info,@content) = split (' ',$line);

		my $text =  join(' ',@content);

		if ($info eq 'pre'){

			if ($text =~ /^\^/){
				$text =~ s/^\^//g;
				$start = 1;
			}
			$pre = $text;
		}
		
		if ($info eq 'regex'){
			$regex = $text;
		}
		
		if ($info eq 'type'){
			$type = $text;
		}

		if ($info eq 'process'){
			my %yaml =(
				'regex'=>$regex,
				'type'=>$type,
				'prefix'=>$pre,
				'start'=>$start
			);
			$prefix{$pre}=1;
			my @config = $configs{$regex};
			@config = [] unless (@config);
			push @config, %yaml;
			$configs{$regex}= @config;
			$regex = undef;
			$pre = undef;
			$type = undef;
			$start = undef;
			#printYAML(%yaml);
		}

	}
}
my $count = 1;
my $PROCESS = 'PROCESS';
foreach my $key (keys %prefix){
	$prefix{$key} = $count ;	
	print "\t".$PROCESS . "_$count $key\n";
	$count++;
}

foreach my $key (keys %configs){

	my @config = $configs{$key};
	print $config[0];
}


close IN;

exit 0;
sub help{
	print HELP;
}

sub printYAML{
	my (%yaml) = @_;
	print "--\n";
	foreach my $key (keys %yaml){
		print $key . " " . $yaml{$key} . "\n" ;
	}
	print "--\n";
	
}
