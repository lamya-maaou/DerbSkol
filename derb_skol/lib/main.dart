import 'package:flutter/material.dart';
import 'screens/dashboard.dart';
import 'screens/login.dart';

void main() {
  runApp(DerbSkolApp());
}

class DerbSkolApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SchoolManager Pro',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.blue),
      home: LoginPage(), // Page de login au démarrage
    );
  }
}
