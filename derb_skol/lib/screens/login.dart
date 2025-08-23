import 'package:flutter/material.dart';
import 'dashboard.dart';

class LoginPage extends StatelessWidget {
  final TextEditingController emailCtrl = TextEditingController();
  final TextEditingController passCtrl = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text("Connexion", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              TextField(controller: emailCtrl, decoration: InputDecoration(labelText: "Email")),
              TextField(controller: passCtrl, obscureText: true, decoration: InputDecoration(labelText: "Mot de passe")),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  // plus tard on connecte à Firebase ou backend
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(builder: (context) => DashboardPage()),
                  );
                },
                child: Text("Se connecter"),
              )
            ],
          ),
        ),
      ),
    );
  }
}
