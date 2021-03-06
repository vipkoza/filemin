#!/usr/bin/perl

require './filemin-lib.pl';
&foreign_require("webmin", "webmin-lib.pl");
use version;

&ReadParse();

&ui_print_unbuffered_header();

# Just in case
if($remote_user eq 'root') {
    my $os = $gconfig{'os_type'};
    my $version = $in{'version'};
    if(index($os, 'linux') != -1) {
        $os = 'linux';
    } elsif (index($os, 'freebsd') != -1){
        $os = 'freebsd';
    } else {
        &error('WHAT???');
    }
    my $url = "https://github.com/Real-Gecko/filemin/raw/master/distrib/filemin-$version.$os.wbm.gz";
    my $tempfile = transname();
    my ($host, $port, $page, $ssl) = &parse_http_url($url);
    &http_download($host, $port, $page, $tempfile, undef, \&progress_callback, $ssl);
    $irv = &webmin::install_webmin_module($tempfile);
    if (!ref($irv)) {
        print &text('update_failed', $irv),"<p>\n";
    }
    else {
        print &text('module_updated', "<b>$irv->[0]->[0]</b>", "<b>$irv->[2]->[0]</b>"),"\n";
    }
}

&ui_print_footer("/", $text{'index'});
