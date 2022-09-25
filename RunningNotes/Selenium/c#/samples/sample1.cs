using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Edge;
using WebDriverManager.DriverConfigs.Impl;

namespace TestProject1
{
    public class Tests
    {
        IWebDriver driver1,driver2;
        [SetUp]
        public void Setup()
        {
            TestContext.Progress.WriteLine("Setup method");
            new WebDriverManager.DriverManager().SetUpDriver(new ChromeConfig());
            driver1 = new ChromeDriver();
            driver1.Manage().Window.Minimize();

            new WebDriverManager.DriverManager().SetUpDriver(new EdgeConfig());
            driver2 = new EdgeDriver();
            driver2.Manage().Window.Minimize();

        }

        [Test]
        public void Test1()
        {
            driver1.Manage().Window.Maximize();
            driver1.Url = "https://google.com";
            driver1.Url = "https://react.com";
            TestContext.Progress.WriteLine(driver1.Title);
            TestContext.Progress.WriteLine(driver1.Url);
            Assert.Pass();
        }
        [Test]
        public void Test2()
        {
            driver2.Manage().Window.Maximize();
            driver2.Url = "https://youtube.com";
            driver2.Url = "https://facebook.com";
            TestContext.Progress.WriteLine(driver2.Title);
            TestContext.Progress.WriteLine(driver2.Url);
            Assert.Pass();
        }
        [TearDown]
        public void CLoseBrowser()
        {
            driver1.Close();
            driver2.Close();
            TestContext.Progress.WriteLine("Teardown method");

        }
    }
}
