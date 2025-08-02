using CED.RestAPITool.Core;
using CED.RestAPITool.Interfaces;
using System.Configuration;
using System.Net;
using System.Reflection;

namespace CED.RestAPITool.Controllers
{
    public class BaseController : IDisposable
    {
        private readonly HttpListener _listener = new();
        private HttpListenerContext? _context;

        public HttpListenerContext? Context => _context;
        public Dictionary<string, MethodInfo> Methods { get; } = new();

        public BaseController() { }

        ~BaseController() => Dispose();

        public void Dispose()
        {
            if (_listener.IsListening)
            {
                _listener.Stop();
            }
        }

        public async Task StartServer()
        {
            RegisterRoutes();

            _listener.Start();

            _ = Task.Run(() =>
            {
                while (_listener.IsListening)
                {
                    try
                    {
                        _context = _listener.GetContext();
                        HandleRequest(_context);
                    }
                    catch (HttpListenerException e)
                    {
                        if (_context != null && e.ErrorCode == (int)HttpStatusCode.NotFound)
                        {
                            _context.Response.StatusCode = (int)HttpStatusCode.NotFound;
                        }
                    }
                    catch (Exception ex)
                    {
                        if (_context != null)
                        {
                            _context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
                        }
                        Console.WriteLine($"Unexpected error: {ex.Message}");
                    }
                    finally
                    {
                        _context?.Response.Close();
                    }
                }
            });
        }

        private void RegisterRoutes()
        {
            var assembly = Assembly.GetExecutingAssembly();
            var controllers = assembly.DefinedTypes
                .Where(t => t.BaseType?.FullName == typeof(BaseController).FullName);
            _listener.Prefixes.Add($"http://localhost:{ConfigurationManager.AppSettings["Port"]}/");
            foreach (var type in controllers)
            {
                var controllerName = type.Name.Replace("Controller", string.Empty);

                foreach (var method in type.DeclaredMethods.Where(m => m.IsPublic))
                {
                    Methods[$"{controllerName}/{method.Name}".ToLower()] = method;
                }
            }
        }

        private void HandleRequest(HttpListenerContext context)
        {
            if (context.Request.Url != null && !context.Request.Url.AbsolutePath.StartsWith("/api"))
            {
                var filePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "wwwroot", string.Join("/", context.Request.Url.AbsolutePath.Split('/', StringSplitOptions.RemoveEmptyEntries)));
                if (File.Exists(filePath))
                {
                    context.Response.StatusCode = (int)HttpStatusCode.OK;
                    context.Response.ContentType = GetMimeType(filePath);

                    using FileStream fs = File.OpenRead(filePath);
                    context.Response.ContentLength64 = fs.Length;
                    byte [] buffer = new byte[16 * 1024];
                    int read;
                    while ((read = fs.Read(buffer, 0, buffer.Length)) > 0)
                    {
                        context.Response.OutputStream.Write(buffer, 0, read);
                        context.Response.OutputStream.Flush();
                    }
                }
                context.Response.StatusCode = (int)HttpStatusCode.NotFound;
                return;
            }

            var pathSegments = context.Request.Url?.AbsolutePath
                .Split('/', StringSplitOptions.RemoveEmptyEntries)
                .Skip(1)
                .Take(2)
                .ToArray();

            if (pathSegments?.Length == 2)
            {
                var key = string.Join("/", pathSegments).ToLower();
                ExecuteAction(key);
                return;
            }
            throw new HttpListenerException((int)HttpStatusCode.NotFound, "Not found");
        }

        private void ExecuteAction(string key)
        {
            if (!Methods.TryGetValue(key, out var method) || method == null)
            {
                throw new HttpListenerException((int)HttpStatusCode.NotFound, "Not found");
            }

            var controllerInstance = Activator.CreateInstance(method.DeclaringType!);
            if (controllerInstance == null)
            {
                throw new HttpListenerException((int)HttpStatusCode.NotFound, "Not found");
            }

            // Inject context into the controller instance
            var contextField = method.DeclaringType!.BaseType?.GetField("_context", BindingFlags.NonPublic | BindingFlags.Instance);
            contextField?.SetValue(controllerInstance, _context);

            var parameters = method.GetParameters();
            var args = new object?[parameters.Length];

            for (int i = 0; i < parameters.Length; i++)
            {
                args[i] = GetParameterValue(parameters[i]);
            }

            var result = method.Invoke(controllerInstance, args);
            if (result is IActionResult actionResult)
            {
                actionResult.ExecuteResult(_context);
                return;
            }
            throw new HttpListenerException((int)HttpStatusCode.NotFound, "Not found");
        }

        private object? GetParameterValue(ParameterInfo parameter)
        {
            var stringValue = _context?.Request?.QueryString?[parameter.Name];

            if (!string.IsNullOrEmpty(stringValue))
            {
                try
                {
                    return Convert.ChangeType(stringValue, parameter.ParameterType);
                }
                catch
                {
                    return parameter.DefaultValue;
                }
            }

            if (parameter.DefaultValue is DBNull or null)
                return null;

            try
            {
                return Convert.ChangeType(parameter.DefaultValue, parameter.ParameterType);
            }
            catch
            {
                return null;
            }
        }

        protected JsonResult JsonResult(object data) => new(data);

        private string? GetMimeType(string path)
        {
            if (!StaticFile.TryGetContentType(path, out var contentType))
            {
                return "application/octet-stream";
            }
            return contentType;
        }
    }
}
