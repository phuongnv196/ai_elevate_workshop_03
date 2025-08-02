using CED.RestAPITool.Interfaces;
using Newtonsoft.Json;
using System.Net;
using System.Text;

namespace CED.RestAPITool.Core
{
    public class JsonResult : IActionResult
    {
        public object? Value { get; set; }

        public JsonResult(object value)
        {
            this.Value = value;
        }

        public async void ExecuteResult(HttpListenerContext context)
        {
            context.Response.StatusCode = (int)HttpStatusCode.OK;
            context.Response.ContentType = "application/json";
            await context.Response.OutputStream.WriteAsync(Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(this.Value, Formatting.Indented)));
            await context.Response.OutputStream.FlushAsync();
        }
    }
}
