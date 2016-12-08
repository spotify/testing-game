using System;
using System.Threading;
using System.Threading.Tasks;
using NUnit.Framework;

namespace Tests
{
    [TestFixture]
    public class TestClass
    {
        [SetUp]
        public void SetUp()
        {
        }

        [Test]
        [ExpectedException(ExpectedException = typeof(NotSupportedException), ExpectedMessage = "negative",
            MatchType = MessageMatch.Contains)]
        public void TestExceptionMultiline()
        {
            throw new NotSupportedException("negative");
        }

        [Test]
        public async void TestAsync()
        {
            await Task.Start(() => {});
        }

        [Test]
        private void UndiscoverablePrivateTest()
        {
            // This test is undiscoverable by NUnit Adapter too
            Assert.That(true, Is.True);
        }

        [Test]
        [Ignore("Test failing on System.OperationCanceledException : The operation was canceled. instead")]
        [ExpectedException( ExpectedException = typeof(TaskCanceledException))]
        public void TestIgnoreAndExpectedException()
        {
            throw new TaskCanceledException();
        }
    }
}