#import <XCTest/XCTestCase.h>

#include <string>

@interface XCTestExampleTest : XCTestCase

@end

@implementation XCTestExampleTest

- (void)setUp
{
    [super setUp];
}

- (void)tearDown
{
    [super tearDown];
}

- (void)testExample
{
    std::string string1("thing");
    std::string string2("thing");
    XCTAssertEqual(string1, string2)
}

@end
