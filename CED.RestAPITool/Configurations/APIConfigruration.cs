using CED.RestAPITool.Controllers;
using Microsoft.Extensions.DependencyInjection;
using System.Reflection;

namespace CED.RestAPITool.Configurations
{
    public static class APIConfigruration
    {
        public static IServiceCollection AddAPIControllers(this IServiceCollection services)
        {
            var assembly = Assembly.GetExecutingAssembly();
            var controllers = assembly.DefinedTypes.Where(x => x.BaseType != null && x.BaseType.FullName == typeof(BaseController).FullName).ToList();
            controllers.ForEach(x => {
                if (x.BaseType != null) services.AddScoped(x.BaseType, x);
            });
            services.AddSingleton<BaseController>();
            return services;
        }
    }
}
