include "test.arc" 		  /* import arc file */
include <"c_injection.c"> /* import c file */
include <Math> 			  /* import native library file */

var string_test = "Hello, world";
var test_ident_define = string_test;

var signed_char = -30;
var unsigned_char = 150;
var unsigned_int = -30000;
var signed_int = 65500;
var unsigned_long = -1000000;
var signed_long = 3000000000;

var test_equation_one = 2+5-7;
var test_equation_two = (3+5*7/11);

var test = 0 && 0 || 1;

function is_even(number) {
	return number % 2 == 0;
}