using CED.RestAPITool.Configurations;
using CED.RestAPITool.Controllers;
using Microsoft.Extensions.DependencyInjection;

namespace CED.RestAPITool
{
    internal static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            // To customize application configuration such as set high DPI settings or default font,
            // see https://aka.ms/applicationconfiguration.
            ApplicationConfiguration.Initialize();

            var services = new ServiceCollection();
            services.AddSingleton<MainForm>();
            services.AddAPIControllers();
            var serviceProvider = services.BuildServiceProvider();
            var form = serviceProvider.GetRequiredService<MainForm>();
            var controller = serviceProvider.GetRequiredService<BaseController>();

            if (form is not null)
            {
                if (controller is not null)
                {
                    controller.StartServer();
                }
                Application.Run(form);
            }
        }
    }
}