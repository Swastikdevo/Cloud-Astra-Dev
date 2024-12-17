```dart
import 'package:flutter/material.dart';
import 'dart:math';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Random Color App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: RandomColorScreen(),
    );
  }
}

class RandomColorScreen extends StatefulWidget {
  @override
  _RandomColorScreenState createState() => _RandomColorScreenState();
}

class _RandomColorScreenState extends State<RandomColorScreen> {
  Color _randomColor = Colors.white;

  void _changeColor() {
    setState(() {
      _randomColor = Color((Random().nextDouble() * 0xFFFFFF).toInt()).withOpacity(1.0);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Random Color Generator'),
      ),
      body: Container(
        color: _randomColor,
        child: Center(
          child: ElevatedButton(
            onPressed: _changeColor,
            child: Text('Change Color'),
          ),
        ),
      ),
    );
  }
}
```