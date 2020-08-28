import 'package:MainInterface/pages/LoginPage.dart';
import 'package:MainInterface/pages/MainPage.dart';
import 'package:MainInterface/pages/SignUpPage.dart';
import 'package:flutter/material.dart';

void main() => runApp(MaterialApp(
  title: 'Robo Platform',
  theme: ThemeData(
    primarySwatch: Colors.indigo,
  ),
  debugShowCheckedModeBanner: false,

  // initial route for the programme to start
  initialRoute: '/main',

  routes: {
    '/login': (context) => LoginPage(), 
    '/signup': (context) => SignUpPage(),
    '/main': (context) => MainPage(),
  },
));