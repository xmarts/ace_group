================================
Picking and Reservation Strategy
================================

* Allows to automatically build optimal picking routes and apply custom reservation options.

|

Changelog
=========

* 1.0.3 (2022-04-27)
    - [FIX] Fixed reservation and removal strategy on ventor base module ignore force removal strategy on Product Category or/and Location

* 1.0.2 (2021-11-30)
    - [FIX] Fixing issue with compute method for strategy_sequence field on stock.location. That was causing issues in POS module

* 1.0.1 (2021-06-21)
    - Optimized algorithm to pick mixed orders  (products and packages together).
    - General bug fixing and improvements.
