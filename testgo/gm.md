# cluster command

| cmd                                        | 功能                                     | remark |
|--------------------------------------------|------------------------------------------|--------|
| ClusterCommandAddAllGossipTest             | 添加全部短信章节                         |        |
| ClusterCommandExecutorGossipTest           | 添加短信章节                             |        |
| ClusterCommandClearAllGossipTest           | 清理所有短信章节                         |        |
| ClusterCommandClearGossipTest              | 清理指定短信章节                         |        |
| ClusterCommandExecutorActivity             | 更新活动                                 |        |
| ClusterCommandExecutorActorFavorUnlock     | 重载雀士情缘解锁数据 -> 用于解锁雀士情缘 |        |
| ClusterCommandExecutorAnnounce             | 刷新公告                                 |        |
| ClusterCommandExecutorClearChallenge       | 清除在线玩家的排行榜数据                 |        |
| ClusterCommandExecutorDisconnect           | 强制断开链接                             |        |
| ClusterCommandExecutorDisconnectAll        | 所有玩家强制断开链接                     |        |
| ClusterCommandExecutorPrivilege            | 修改玩家权限 && 重新登陆                 |        |
| ClusterCommandExecutorRefreshCDKey         | 刷新兑换码配置                           |        |
| ClusterCommandExecutorRefreshGoodReview    | 刷新好评配置                             |        |
| ClusterCommandExecutorRefreshJoinGroup     | 刷新加群配置                             |        |
| ClusterCommandExecutorRefreshQuestionnaire | 刷新问卷配置                             |        |
| ClusterCommandExecutorReloadEx             | 刷新问卷配置                             |        |
| ClusterCommandReloadDiamondAward           | 刷新勾玉赏奖励配置                       |        |
| ClusterCommandExecutorGameCommand          | 执行gm命令                               |        |

# game command

| cmd                               | 功能                                                           | remark |
|-----------------------------------|----------------------------------------------------------------|--------|
| AchievementClear                  | 重置玩家成就数据                                               |        |
| ActivityDelete                    | 删除指定活动                                                   |        |
| ActivityPostDiscord               | 加群事件                                                       |        |
| ActivityPostGoodReview            | 好评事件                                                       |        |
| ActivityPostQuestionnaireSurvey01 | 问卷事件                                                       |        |
| ActivityRookiesMonthlyUnlock      | 福利月函事件                                                   |        |
| ActivityStart                     | 活动开启命令 增加白名单后几乎不用                              |        |
| ActorChoose                       | 收藏雀士    直接收藏，用途不明                                 |        |
| ActorDelete                       | 删除雀士                                                       |        |
| ActorEmojiAdd                     | 增加emoji                                                      |        |
| ActorFavorAdd                     | 增加雀士情缘值                                                 |        |
| ActorFavorClear                   | 清理雀士情缘 置为空值，情缘置为关闭                            |        |
| ActorFavorExDisable               | 雀士开启情缘                                                   |        |
| ActorFavorExEnable                | 雀士关闭情缘                                                   |        |
| ActorFavorGetAward                | 获取指定等级的情缘奖励                                         |        |
| ActorFavorSiteLevel               | 设置指定等级的情缘                                             |        |
| ActorFlashGiftLimit               | 重置赠送礼物限制的数量                                         |        |
| ActorGiveGift                     | 雀士赠送礼物                                                   |        |
| ActorSmsClear                     | 雀士清理短信状态                                               |        |
| ActorStoryClear                   | 雀士清理故事状态                                               |        |
| ActorSwitch                       | 切换雀士                                                       |        |
| AnnounceRefresh                   | 公告刷新  跟上面相同                                           |        |
| AvatarChoose                      | 收藏皮肤                                                       |        |
| AvatarSwitch                      | 切换皮肤                                                       |        |
| BuyCommand                        | 购买商品                                                       |        |
| ChallengeClearStatus              | 重置挑战赛数据                                                 |        |
| ChallengeGetAward                 | 挑战赛获取奖励                                                 |        |
| ChallengeHandlePlayedResult       | 更新挑战赛数据                                                 |        |
| ChallengeQueryLadderAward         | 查询排名奖励                                                   |        |
| ChallengeQueryRank                | 查询排名                                                       |        |
| ChallengeReadyAward               | 奖励设置为准备发放状态                                         |        |
| ClearAutoMail                     | 清理自动发送邮件                                               |        |
| ClearChallengeResult              | 清理挑战赛状态                                                 |        |
| CompleteSingIn7                   | 7日签到活动                                                    |        |
| DanAddScore                       | 段位赛增加分数                                                 |        |
| DanGetDailyAward                  | 获取段位赛每日奖励                                             |        |
| DanGetLevelAward                  | 获取段位赛等级奖励                                             |        |
| DanHandlePlayedResult             | 更新段位赛数据                                                 |        |
| DanQueryLevelAward                | 查询段位赛等级奖励                                             |        |
| DanQueryRank                      | 查询段位赛排名                                                 |        |
| DanResetDailyAward                | 段位赛重置每日奖励                                             |        |
| DanResetLevelAward                | 段位赛重置等级奖励                                             |        |
| DanSetLevel                       | 段位赛设置等级                                                 |        |
| DanSetTotalScore                  | 段位赛设置得分                                                 |        |
| DefaultGameCommandService         |                                                                |        |
| DiscordClearMember                | 清理加群人数                                                   |        |
| DropCollectLottery                | 抽奖掉落                                                       |        |
| DropGroup                         | 商城掉落                                                       |        |
| FriendAdd                         | 发送增加好友                                                   |        |
| FriendAgree                       | 好友同意                                                       |        |
| FriendDelete                      | 删除好友                                                       |        |
| GameCommand                       |                                                                |        |
| GlobalConfigSetter                | 设置全局变量                                                   |        |
| ItemAdd                           | 增加道具                                                       |        |
| ItemClear                         | 清除所有道具                                                   |        |
| ItemExpire                        | 设置道具有效期                                                 |        |
| ItemRemove                        | 删除指定道具                                                   |        |
| ItemSell                          | 出售道具                                                       |        |
| ItemUse                           | 使用道具                                                       |        |
| Lottery                           | 抽奖                                                           |        |
| MailAdd                           | 增加邮件                                                       |        |
| MailAddChallengeRandMoney         | 邮件发送随机金币                                               |        |
| MailAddChallengeRankAward         | 邮件发送排名奖励                                               |        |
| MailClear                         | 清除玩家邮件                                                   |        |
| MailDeleteAllChecked              | 删除已读邮件                                                   |        |
| MailGet                           | 领取指定邮件                                                   |        |
| MailGetAll                        | 领取所有邮件                                                   |        |
| MailSetChecked                    | 设置邮件已读                                                   |        |
| MoneyAdd                          | 增加货币 增加道具可以覆盖                                      |        |
| MoneyAddCloth                     | 增加服饰币 增加道具可以覆盖                                    |        |
| MoneyAddCoin                      | 增加铜币 增加道具可以覆盖                                      |        |
| MoneyAddDiamond                   | 增加勾玉 增加道具可以覆盖                                      |        |
| MoneyAddToken                     | 增加小鱼干 增加道具可以覆盖                                    |        |
| NotificationReceive               | 取出并处理通知                                                 |        |
| OrnamentChoose                    | 收藏装扮                                                       |        |
| OrnamentSwitch                    | 切换装扮                                                       |        |
| PlayerAuthPlatformUser            | 验证平台用户                                                   |        |
| PlayerChangeLang                  | 更新用户语言                                                   |        |
| PlayerClearQuestionnaire          | 清除问卷提交状态                                               |        |
| PlayerDisconnect                  | 断开链接 如上                                                  |        |
| PlayerExchangeCode                | 使用兑换码                                                     |        |
| PlayerExchangeCodeClear           | 清理兑换码                                                     |        |
| PlayerGetAllItems                 | 把配置表中所有道具添加到玩家，应该是用于检查添加道具是否会出错 |        |
| PlayerLinkAccount                 | 绑定平台                                                       |        |
| PlayerLinkAccountByMailBox        | 绑定邮箱                                                       |        |
| PlayerLogoutAccount               | 注销账号                                                       |        |
| PlayerLogoutAccountByMailBox      |                                                                |        |
| PlayerModifyPassword              |                                                                |        |
| PlayerProductConsumed             |                                                                |        |
| PlayerSendLinkAccountMailCode     |                                                                |        |
| PlayerSendLogoutAccountMailCode   |                                                                |        |
| PlayerSendRetrievePasswordCode    |                                                                |        |
| PlayerSendUnlinkAccountMailCode   |                                                                |        |
| PlayerSetLang                     |                                                                |        |
| PlayerUnlinkAccount               |                                                                |        |
| PlayerUnlinkAccountByMailBox      |                                                                |        |
| ProductExchange                   |                                                                |        |
| PurchasedObtainProduct            |                                                                |        |
| RandomShopFlashCommand            |                                                                |        |
| RandomShopListCommand             |                                                                |        |
| RandomShoppingCommand             |                                                                |        |
| RechargeClearProducts             |                                                                |        |
| RechargeClearVersion              |                                                                |        |
| RechargePushProduct               |                                                                |        |
| ReplayShare                       |                                                                |        |
| ResetGm                           |                                                                |        |
| ResetNoviceGiftActivity           |                                                                |        |
| RoomCreate                        |                                                                |        |
| SetDailyResetTime                 |                                                                |        |
| ShoppingCommand                   |                                                                |        |
| SitePlayerLevel                   |                                                                |        |
| TitleChoose                       |                                                                |        |
| TitleSwitch                       |                                                                |        |
