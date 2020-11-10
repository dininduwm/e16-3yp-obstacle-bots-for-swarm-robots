import 'package:MainInterface/support/BotStatusCard.dart';
import 'package:MainInterface/support/DragBox.dart';
import 'package:flutter/material.dart';

class MainPage extends StatefulWidget {
  MainPage({Key key}) : super(key: key);

  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  ///bot status card array
  List<BotStatusCard> botCards = [
    new BotStatusCard("Bot one"),
    new BotStatusCard("Bot two"),
    new BotStatusCard("Bot three"),
  ];

  @override
  Widget build(BuildContext context) {
    ///center canves size
    double sizeOfCanves = MediaQuery.of(context).size.height * 0.95;
    // starting point of the canves
    double startingPoint =
        MediaQuery.of(context).size.width - 20 - sizeOfCanves;

    return Scaffold(
      body: Stack(
        children: [
          Container(
            decoration: BoxDecoration(
              image: DecorationImage(
                image: AssetImage('assets/background.jpg'),
                fit: BoxFit.cover,
              ),
            ),
          ),
          Center(
            child: Row(
              children: [
                SizedBox(
                  width: 20.0,
                ),
                Expanded(
                  child: ListView.builder(
                    padding: EdgeInsets.only(
                      top: 20.0,
                    ),
                    itemCount: botCards.length,
                    itemBuilder: (BuildContext botCard, int index) {
                      return botCards[index];
                    },
                  ),
                ),
                SizedBox(
                  width: 20.0,
                ),
                Card(
                  child: Container(
                    height: sizeOfCanves,
                    width: sizeOfCanves,
                    child: Stack(
                      children: [
                        DragBox(Offset(0.0, 0.0), 'Bot One', Colors.blueAccent,
                            startingPoint),
                        DragBox(Offset(200.0, 0.0), 'Bot Two', Colors.orange,
                            startingPoint),
                        DragBox(Offset(400.0, 0.0), 'Bot Three',
                            Colors.lightGreen, startingPoint),
                        Positioned(
                          bottom: 5.0,
                          right: 10.0,
                          child: RaisedButton(
                            color: Colors.indigo,
                            onPressed: () {},
                            child: Row(
                              children: [
                                Icon(
                                  Icons.send,
                                  color: Colors.white,
                                ),
                                SizedBox(width: 5.0),
                                Text("Deploy Obstacal Bots",
                                style: TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold,
                                ),),
                              ],
                            ),
                          ),
                        )
                      ],
                    ),
                  ),
                ),
                SizedBox(
                  width: 20.0,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
