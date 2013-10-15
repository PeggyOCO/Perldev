#!/usr/local/bin/perl
print "Content-type: text/html\n\n";

use warnings;
use strict;

my $xml ='<?xml version="1.0" encoding="UTF-8"?>
<TEST xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<TEST1>
<ID>1223</ID>
<DESCRIPTION>XXXXX</DESCRIPTION>
</TEST1>
</TEST>
';


use LWP::UserAgent;
my $curl = LWP::UserAgent->new( timeout => 120 );

my $url = "http://www.mariposagraphics.com/testperl/testxsdresp.cgi";
my $response = $curl->post($url, Content => $xml);

if ($response->is_success) {
     print $response->decoded_content;  # or whatever
}
else {
    print $response->status_line;
}
  #$output->close();

#my $xsd = 'ship-val-global-req.xsd';

#my $schema = XML::Compile::Schema->new($xsd);

# This will print a very basic description of what the schema describes
#$schema->printIndex();

# this will print a hash template that will show you how to construct a 
# hash that will be used to construct a valid XML file.
#
# Note: the second argument must match the root-level element of the XML 
# document.  I'm not quite sure why it's required here.
#warn $schema->template('PERL', 'ShipmentRequest');



 