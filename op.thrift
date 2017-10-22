enum PokerColor
{
    diamond = 0,
    club = 1,
    heart = 2,
    spade = 3
}

struct Poker
{
    1: required i8 v;//value
    2: required PokerColor t;//color   
}

service ReqService{

    bool login(1:string name,2:string pw),//登陆
    void startPlay(), //开始游戏
    list<Poker> dealCards(), //发牌
    Poker askForCards(),//要牌
}
