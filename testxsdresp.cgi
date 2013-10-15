#!/usr/local/bin/perl
print "Content-type: text/html\n\n";

use strict;
use XML::Simple;
use Data::Dumper;
my $simple = XML::Simple->new();
my $data   = $simple->XMLin('test.xml');
# DEBUG

print Dumper($data) . "\n";


print "$data->{cat}->{name} was born  $data->{cat}->{dob} years old and the dog Maggie's owner is:  $data->{dog}->{Maggie}->{owner}\n";

# END


#use CGI qw(:cgi-lib :standard);  # Use CGI modules that let people read data passed from a form


	#&ReadParse(%in);                 # This grabs the data passed by the form and puts it in an array
	
	#$name = $in{"name"};             # Get the user's name and assign to variable
	#$preference = $in{"choice"};     # Get the choice and assign to variable
	
	                                 # Start printing HTML document
	#print "
	
	#<HTML>
	#<BODY BGCOLOR=WHITE TEXT=BLACK>
	#<H1> Hello, $name </H1>          <!-- Use variables in HTML text -->
	#You prefer  $preference.
	#<BR>
	#";
	
	#for ($i=1; $i<=5; $i++)          # Print name 5 times
	# {print "$i. $name <BR>";}
	
	#print "
	#</BODY>
	#</HTML>
	#";