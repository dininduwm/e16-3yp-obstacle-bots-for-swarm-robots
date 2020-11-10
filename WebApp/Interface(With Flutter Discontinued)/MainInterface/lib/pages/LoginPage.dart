import 'package:flutter/material.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({Key key}) : super(key: key);

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  TextEditingController tpCon = TextEditingController(),
      passCon = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.green,
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
          Row(
            children: [
              SizedBox(
                width: MediaQuery.of(context).size.width * 0.55,
              ),
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.fromLTRB(10, 50.0, 100.0, 50.0),
                  child: Card(
                    color: Colors.white.withOpacity(0.6),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.all(Radius.circular(50)),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: ListView(
                        children: [
                          Row(
                            children: [
                              Column(
                                children: [
                                  Container(
                                    padding: EdgeInsets.only(left: 20.0),
                                    alignment: Alignment.centerLeft,
                                    child: Text(
                                      "Hello",
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 50.0,
                                        color: Colors.indigo[800],
                                      ),
                                    ),
                                  ),
                                  Container(
                                    padding: EdgeInsets.only(left: 20.0),
                                    alignment: Alignment.centerLeft,
                                    child: Text(
                                      "There...",
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 60.0,
                                        color: Colors.indigo[800],
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                              Expanded(
                                child: Padding(
                                  padding: const EdgeInsets.all(10.0),
                                  child: Image.asset(
                                    'assets/welcomebot.png',
                                    height: 120,
                                  ),
                                ),
                              ),
                            ],
                          ),
                          Container(
                            padding: EdgeInsets.only(
                                top: 0.0, left: 20.0, right: 20.0),
                            child: Column(
                              children: <Widget>[
                                SizedBox(
                                  height: 20.0,
                                ),
                                TextField(
                                  decoration: InputDecoration(
                                    labelText: 'EMAIL',
                                    labelStyle: TextStyle(
                                        fontFamily: 'Montserrat',
                                        fontWeight: FontWeight.bold,
                                        color: Colors.indigo),
                                    border: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(20),
                                    ),
                                  ),
                                ),
                                SizedBox(height: 20.0),
                                TextField(
                                  decoration: InputDecoration(
                                    labelText: 'PASSWORD',
                                    labelStyle: TextStyle(
                                        fontFamily: 'Montserrat',
                                        fontWeight: FontWeight.bold,
                                        color: Colors.indigo),
                                    border: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(20),                            
                                    ),
                                  ),
                                  obscureText: true,
                                ),
                                SizedBox(height: 5.0),
                                Container(
                                  alignment: Alignment(1.0, 0.0),
                                  padding:
                                      EdgeInsets.only(top: 15.0, left: 20.0),
                                  child: InkWell(
                                    child: Text(
                                      'Forgot Password',
                                      style: TextStyle(
                                          color: Colors.indigo,
                                          fontWeight: FontWeight.bold,
                                          fontFamily: 'Montserrat',
                                          decoration: TextDecoration.underline),
                                    ),
                                  ),
                                ),
                                SizedBox(height: 40.0),
                                GestureDetector(
                                  onTap: () {
                                    print("Login Clicked");
                                  },
                                  child: Container(
                                    height: 40.0,
                                    child: Material(
                                      borderRadius: BorderRadius.circular(20.0),
                                      shadowColor: Colors.greenAccent,
                                      color: Colors.indigo,
                                      elevation: 7.0,
                                      child: Center(
                                        child: Text(
                                          'LOGIN',
                                          style: TextStyle(
                                              color: Colors.white,
                                              fontWeight: FontWeight.bold,
                                              fontFamily: 'Montserrat'),
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                                SizedBox(height: 20.0),
                              ],
                            ),
                          ),
                          SizedBox(height: 15.0),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: <Widget>[
                              Text(
                                'New to Swarm Robot Platform ?',
                                style: TextStyle(fontFamily: 'Montserrat'),
                              ),
                              SizedBox(width: 5.0),
                              InkWell(
                                onTap: () {
                                  Navigator.of(context).pushNamed('/signup');
                                },
                                child: Text(
                                  'Register',
                                  style: TextStyle(
                                    color: Colors.indigo,
                                    fontFamily: 'Montserrat',
                                    fontWeight: FontWeight.bold,
                                    decoration: TextDecoration.underline,
                                  ),
                                ),
                              )
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
