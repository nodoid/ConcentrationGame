using Foundation;

namespace Concentration
{
    // iOS / Mac Catalyst 27 no longer launch apps without the UIScene life cycle;
    // the scene manifest in Info.plist names this class.
    [Register("SceneDelegate")]
    public class SceneDelegate : MauiUISceneDelegate
    {
    }
}
