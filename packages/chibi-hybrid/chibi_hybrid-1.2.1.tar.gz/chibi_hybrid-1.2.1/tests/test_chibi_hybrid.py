#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from chibi_hybrid import Chibi_hybrid, Class_property


class Dump:
    __bar = ''

    def __init__( self, value ):
        self.value = value

    @Chibi_hybrid
    def foo( cls ):
        return cls( 'cls' )

    @foo.instancemethod
    def foo( self ):
        return self.value

    @Class_property
    def bar( cls ):
        return cls.__bar

    @bar.setter
    def bar( cls, value ):
        cls.__bar = value

    @bar.instance
    def bar( self ):
        return self.value


class Inner_reason_fail:
    def __init__( self, parent ):
        self.parent = parent


class Reason_fail( str ):
    schema = 'http'
    host = None

    def __init__( self ):
        self._API = Inner_reason_fail( self )

    @Class_property
    def API( cls ):
        return cls().API

    @API.instance
    def API( self ):
        return self._API



class Test_chibi_hybrid( unittest.TestCase ):
    def test_should_work( self ):
        result = Dump.foo()
        self.assertIsInstance( result, Dump )
        self.assertEqual( 'cls', result.value )
        self.assertEqual( 'cls', result.foo() )

        result = Dump( 'cosa' ).foo()
        self.assertEqual( 'cosa', result )

    def test_should_work_the_property_class( self ):
        self.assertEqual( Dump.bar, '' )
        Dump.bar = "cosa 2"
        self.assertEqual( Dump.bar, 'cosa 2' )

    def test_instance_property_should_work( self ):
        self.assertEqual( Dump.bar, '' )
        dump = Dump( "cosa 2" )
        self.assertEqual( dump.bar, 'cosa 2' )
        self.assertEqual( Dump.bar, '' )


class Test_reason_fail( unittest.TestCase ):
    def test_should_work( self ):
        result = Reason_fail.API
        result2 = Reason_fail.API
        self.assertTrue( result )
        self.assertIsNot( result, result2 )

        reason = Reason_fail()
        instance_result = reason.API
        instance_result2 = reason.API
        self.assertIs( instance_result, instance_result2 )
        self.assertIsNot( instance_result, result )
