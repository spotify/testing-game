#import <Foundation/Foundation.h>

#include <boost/optional.hpp>
#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_SUITE(spotify)
BOOST_AUTO_TEST_SUITE(testinggame)

BOOST_AUTO_TEST_CASE(BoostTestExample) {
    NSString *string1 = @"a";
    NSString *string2 = @"a";
    BOOST_CHECK([string1 isEqualToString:string2]);
}

BOOST_AUTO_TEST_SUITE_END()
BOOST_AUTO_TEST_SUITE_END()
