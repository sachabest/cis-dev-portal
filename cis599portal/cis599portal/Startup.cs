using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(cis599portal.Startup))]
namespace cis599portal
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            ConfigureAuth(app);
        }
    }
}
