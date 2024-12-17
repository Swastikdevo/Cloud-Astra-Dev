```dart
import 'package:flutter/material.dart';

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

  void _generateRandomColor() {
    setState(() {
      _randomColor = Color((Math.Random().nextDouble() * 0xFFFFFF).toInt()).withAlpha(0xFF);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Random Color Generator'),
      ),
      body: Center(
        child: GestureDetector(
          onTap: _generateRandomColor,
          child: Container(
            width: 200,
            height: 200,
            color: _randomColor,
            child: Center(
              child: Text(
                'Tap me!',
                style: TextStyle(color: Colors.black, fontSize: 24),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
```