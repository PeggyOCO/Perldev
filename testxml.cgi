#!/usr/local/bin/perl
print "Content-type: text/html\n\n";

# use module
use XML::Simple;
use Data::Dumper;

# create object
$xml = new XML::Simple;

# read XML file
$data = $xml->XMLin("test.xml");

# print output
print Dumper($data);