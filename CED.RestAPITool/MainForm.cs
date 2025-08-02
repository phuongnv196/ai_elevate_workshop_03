
using Microsoft.Web.WebView2.WinForms;
using System.Configuration;

namespace CED.RestAPITool
{
    public partial class MainForm : Form
    {
        public MainForm(IServiceProvider services)
        {
            var webView = new WebView2
            {
                Dock = DockStyle.Fill,
                Source = new Uri($"http://localhost:{ConfigurationManager.AppSettings["Port"]}/index.html")
            };

            Controls.Add(webView);
            InitializeComponent();
        }
    }
}
