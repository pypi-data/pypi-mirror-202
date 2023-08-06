package Javonet::Core::Handler::CommandHandler::ArrayGetRankHandler;
use aliased 'Javonet::Core::Handler::PerlHandler' => 'PerlHandler';
use strict;
use warnings FATAL => 'all';
use Moose;
use lib 'lib';
use lib 'data_seed';
use Nice::Try;
use aliased 'Javonet::Core::Handler::Exception' => 'Exception';
extends 'Javonet::Core::Handler::CommandHandler::AbstractCommandHandler';

sub new {
    my $class = shift;
    my $self = {
        required_parameters_count => 1
    };
    return bless $self, $class;
}

sub process {
    my ($self, $command) = @_;
    try {
        die Javonet::Core::Handler::Exception->new("ArrayGetRankHandler not implemented");
    }
    catch ( $e ) {
        return $e;
    }
}

no Moose;
1;
