#!/usr/local/bin/perl
print "Content-type: text/html\n\n";

package MyClass;

use CGI; 
$q = new CGI;
my $value = $q->param('test');

print $value;
print '<hr>';

sub new
{
   print "<html><head><title></title></head><body>";
   my $type = shift;            # The package/type name
   my $self = {};               # Reference to empty hash
   
   return bless $self, $type;   
}

sub DESTROY
{
   print " <h2> Perl Test</h2>";
}

sub MyMethod
{
   print "   got here to method <br>";
}


package MySubClass;

@ISA = qw( MyClass );

sub new
{
   print "   got here to subclass <br>";
   my $type = shift;            # The package/type name
   my $self = MyClass->new;     # Reference to empty hash
   return bless $self, $type;  
}

sub DESTROY
{
   print "   destroy, save memory<br>";
}

sub MyMethod
{
   my $self = shift;
   $self->SUPER::MyMethod();
   print "   subclass <br>";
}

# Here is the main program using above classes.
package main;

print "Invoke MyClass method<br>";

$myObject = MyClass->new();
$myObject->MyMethod();

print "Invoke MySubClass method<br>";

$myObject2 = MySubClass->new();
$myObject2->MyMethod();

print "Create a scoped object<br>";
{
	my $myObject2 = MyClass->new();
}


print "Create and undefine an object<br>";
$myObject3 = MyClass->new();
undef $myObject3;

print "Fall off the end of the script...<br></body></html>";
