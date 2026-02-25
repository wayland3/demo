// let s1 = `{"_host":"mahjong-maque-server-game2-76c767cd95-zggw9","_saddr":"60:3:2","_transaction":80,"duration":273,"error":"runtime error: invalid memory address or nil pointer dereference","route":{"name":"handlerGDLinkPlatformUserAns","subCode":4,"topCode":7},"serviceAddr":"60:2:1","serviceName":"data-1","stack":"goroutine 558 [running]:\nruntime/debug.Stack()\n\truntime/debug/stack.go:24 +0x5e\nmaque-server/pkg/server.(*messageRouter).Handle.func2.1()\n\tmaque-server/pkg/server/router.go:177 +0x130\npanic({0x120e860?, 0x2001160?})\n\truntime/panic.go:914 +0x21f\nmaque-server/pkg/services/game/internal/moduler/account.(*Moduler).LinkPlatformUserAns(0xc0005a64d0, {0x163ec88, 0xc000991770}, 0xc0009f52c0)\n\tmaque-server/pkg/services/game/internal/moduler/account/gd_link_platform_user_ans.go:33 +0xa4\nmaque-server/pkg/services/game.(*Application).Initialize.(*Application).handlerGDLinkPlatformUserAns.func16({0x163ec88, 0xc000991770}, {0xffffffffffffffff?, 0xffffffffffffffff?}, {0x1317bc0?, 0xc0009f52c0?})\n\tmaque-server/pkg/services/game/data_handlers.go:96 +0x65\nmaque-server/pkg/server.(*messageRouter).Handle.func2()\n\tmaque-server/pkg/server/router.go:187 +0x183\ngithub.com/bytedance/gopkg/util/gopool.(*worker).run.func1.1(0xc02451?, 0xc000b3ae60?)\n\tgithub.com/bytedance/gopkg@v0.0.0-20230728082804-614d0af6619b/util/gopool/worker.go:69 +0x57\ngithub.com/bytedance/gopkg/util/gopool.(*worker).run.func1()\n\tgithub.com/bytedance/gopkg@v0.0.0-20230728082804-614d0af6619b/util/gopool/worker.go:70 +0xe9\ncreated by github.com/bytedance/gopkg/util/gopool.(*worker).run in goroutine 172\n\tgithub.com/bytedance/gopkg@v0.0.0-20230728082804-614d0af6619b/util/gopool/worker.go:41 +0x4f\n"}`
var s = "hel\t\nlo";
// raw字符串转为普通字符串
function rawStringToNormalString(rawString) {
    return rawString.replace(/\\[0-9a-f]{4}/g, function (match) {
        return String.fromCharCode(parseInt(match.replace('\\u', ''), 16));
    });
}
s = rawStringToNormalString(s);
console.log(s);
