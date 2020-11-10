import 'package:flutter/material.dart';

class BotStatusCard extends StatefulWidget {
  ///botname
  String botName;

  ///constructor for the bot class
  BotStatusCard(this.botName);

  @override
  _BotStatusCardState createState() => _BotStatusCardState();
}

class _BotStatusCardState extends State<BotStatusCard> {
  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.white.withOpacity(0.6),
      child: Container(
        height: 200.0,
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Row(
            children: [
              Image.asset('assets/Assembled.png'),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Column(
                  children: [
                    Text(
                      widget.botName + " Status",
                      style: TextStyle(
                        color: Colors.indigo,
                        fontWeight: FontWeight.bold,
                        fontSize: 25.0,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
