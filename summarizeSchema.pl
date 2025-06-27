#!/usr/bin/perl
use strict;
use warnings;

my $models_dir = "backend/models";
my $schema_file = "backend/docker/dumps/init.sql";

# Read schema content
open(my $schema_fh, '<', $schema_file) or die "Could not open $schema_file: $!";
my $schema_content = do { local $/; <$schema_fh> };
close($schema_fh);

# Open models directory
opendir(my $dir, $models_dir) or die "Cannot open directory $models_dir: $!";
my @model_files = grep { /\.py$/ && $_ ne '__init__.py' } readdir($dir);
closedir($dir);

my @missing_tables;

foreach my $file (@model_files) {
    my $path = "$models_dir/$file";

    open(my $fh, '<', $path) or die "Could not open $path: $!";

    my $table_name;
    while (my $line = <$fh>) {
        if ($line =~ /__tablename__\s*=\s*["'](\w+)["']/) {
            $table_name = $1;
            last;
        }
    }
    close($fh);

    if (defined $table_name) {
        if ($schema_content =~ /\bCREATE TABLE `$table_name`/i || $schema_content =~ /\bCREATE TABLE $table_name\b/i) {
            print "[✓] Found table '$table_name' defined in $file\n";
        } else {
            print "[✗] Table '$table_name' from $file NOT FOUND in init.sql\n";
            push @missing_tables, $file;
        }
    } else {
        print "[!] No __tablename__ found in $file\n";
    }
}

if (@missing_tables) {
    print "\nSome models reference tables not found in schema:\n";
    print "  - $_\n" for @missing_tables;
    exit 1;
} else {
    print "\nAll model tables matched successfully in schema ✅\n";
    exit 0;
}
