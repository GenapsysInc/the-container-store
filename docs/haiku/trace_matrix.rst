Verification Trace Matrix
*********************************

Purpose
=======

This document provides the tracing from Requirement to Test Case. Need some change.

Scope
=====

This document only provides the tracing the test case execution result is reported on the Verification Execution Report for this module



Trace Matrix
============

.. item-matrix:: Requirements to test cases
   :source: REQ
   :target: TEST
   :sourcetitle: Software requirements
   :targettitle: Unit test cases
   :stats:

..   :coverage: == 100

.. item-matrix:: UN to requirement traceability
    :source: UN
    :target: REQ
    :type: fulfilled_by



.. item-matrix:: UN to test case via requirement traceability
    :source: UN
    :intermediate: REQ
    :target: TEST
    :type: fulfilled_by | validated_by
    :intermediatetitle: Requirements
    :sourcetitle: User Needs
    :targettitle: Test cases
    :splitintermediates:
    :stats:

.. item-matrix:: UN to test case via requirement traceability
    :source: UN
    :intermediate: REQ
    :target: TEST
    :type: fulfilled_by | validated_by
    :sourcetitle: User Needs
    :targettitle: Test cases
    :splitintermediates:
    :stats:


.. item-2d-matrix:: Requirements to test case description traceability
    :source: REQ
    :target: TEST
    :type: validated_by fulfilled_by
    :hit: x
    :miss:
