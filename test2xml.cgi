#!/usr/local/bin/perl
print "Content-type: text/html\n\n";


#use SOAP::Lite trace=>'debug';
use strict;

use XML::Simple;
use Date::Calc qw(Add_Delta_YM Decode_Date_EU Delta_Days Delta_YMD); 
use Data::Dumper;

my $simple = XML::Simple->new (ForceArray => 1, KeepRoot => 1);
my $data   = $simple->XMLin('test.xml');

my @now = (localtime(time))[5, 4, 3];
$now[0] += 1900;  # Perl years start in 1900
$now[1]++;        # months are zero-based

sub fixPrice($$) {
    my ($amt, $change) = @_;
    return sprintf "%6.2f", $amt * (1 + $change);
}

sub deltaYMD($$) {
    my ($earlier, $later) = @_;   # refs to YMD arrays
    my @delta = Delta_YMD (@$earlier, @$later); 
    while ( $delta[1] < 0 or $delta[2] < 0 ) {
        if ( $delta[1] < 0 ) {  # negative month
            $delta[0]--;
            $delta[1] += 12;
        }
        if ( $delta[2] < 0 ) {  # negative day
            $delta[1]--;
            $delta[2] = Delta_Days(
                    Add_Delta_YM (@$earlier, @delta[0,1]), @$later);
        }
    }
    return \@delta;
}
 
sub dob2age($) {
    my $strDOB = shift;
    my @dob = Decode_Date_EU($strDOB);
    my $ageRef = deltaYMD( \@dob, \@now );
    my ($ageYears, $ageMonths, $ageDays) = @$ageRef;
    my $age;
    if ( $ageYears > 1 ) {
        $age = "$ageYears years"; 
    } elsif ($ageYears == 1) {
        $age = '1 year' . ( $ageMonths > 0 ? 
            ( ", $ageMonths month" . ($ageMonths > 1 ? 's' : '') ) 
            : '');
    } elsif ($ageMonths > 1) {
        $age = "$ageMonths months";
    } elsif ($ageMonths == 1) {
        $age = '1 month' . ( $ageDays > 0 ?
            ( ", $ageDays day" . ($ageDays > 1 ? 's' : '') ) : '');
    } else {
        $age = "$ageDays day" . ($ageDays != 1 ? 's' : '');
    }
    return $age;

}
 
sub makeNewHash($) {
    my $hashRef = shift;
    my %oldHash = %$hashRef;
    my %newHash = ();
    while ( my ($key, $innerRef) = each %oldHash ) {
        my $value = @$innerRef[0];
        if ($key eq 'dob') {
            $newHash{'age'} = dob2age($value);
        } else {
            if ($key eq 'price') {
                $value = fixPrice($value, 0.20);
            }
            $newHash{$key} = $value;
        }
    }
    return \%newHash;
}
sub foldType ($) {
    my $arrayRef = shift;
    # if single element in array, return simple hash
    if (@$arrayRef == 1) { 
        return makeNewHash(@$arrayRef[0]);
    }
    # if multiple elements, return array of simple hashes
    else {
        my @outArray = ();
        foreach my $hashRef (@$arrayRef) {
            push @outArray, makeNewHash($hashRef);
        }
        return \@outArray;
    }
} 
my $dispatcher = {
    'cat' => sub { foldType(shift); }, 
    'dog' => sub { foldType(shift); },
};
 
my @base = @{$data->{pets}};
my %types = %{$base[0]};
my %newTypes = ();
while ( my ($petType, $arrayRef) = each %types ) {
    my @petArray = @$arrayRef;
    print "type $petType has " . @petArray . " representatives \n";
 
    my $refReturned = &{$dispatcher->{$petType}}( $arrayRef );
    $newTypes{$petType} = $refReturned;
}
$data->{pets} = \%newTypes;             # overwrite existing data
$simple->XMLout($data, 
            KeepRoot   => 1, 
            OutputFile => 'pets.fixed.xml',
            XMLDecl    => "<?xml version='1.0'?>",
        );