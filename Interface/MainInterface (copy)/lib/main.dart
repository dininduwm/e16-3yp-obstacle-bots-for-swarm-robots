import 'package:flutter/material.dart';
import 'pages/LoginPage.dart';

void main() => runApp(MaterialApp(
  debugShowCheckedModeBanner: false,

  initialRoute: '/login',

  routes: {
    '/login': (context) => LoginPage(), 
  },
));