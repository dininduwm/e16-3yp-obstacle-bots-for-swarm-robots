import 'dart:js';

import 'package:MainInterface/pages/LoginPage.dart';
import 'package:MainInterface/pages/SignUpPage.dart';
import 'package:flutter/material.dart';

void main() => runApp(MaterialApp(
  title: 'Robo Platform',
  debugShowCheckedModeBanner: false,

  // initial route for the programme to start
  initialRoute: '/login',

  routes: {
    '/login': (context) => LoginPage(), 
    '/signup': (context) => SignUpPage(),
  },
));