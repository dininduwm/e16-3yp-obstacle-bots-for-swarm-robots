import 'package:flutter/material.dart';
import 'pages/LoginPage.dart';

void main() => runApp(MaterialApp(
  title: 'Robo Platform',
  debugShowCheckedModeBanner: false,

  // initial route for the programme to start
  initialRoute: '/login',

  routes: {
    '/login': (context) => LoginPage(), 
  },
));