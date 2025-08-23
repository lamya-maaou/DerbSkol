import 'package:flutter/material.dart';

class DashboardPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("SchoolManager Pro"),
        backgroundColor: Colors.blue,
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(color: Colors.blue),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.school, size: 50, color: Colors.white),
                  SizedBox(height: 10),
                  Text(
                    "Menu Principal",
                    style: TextStyle(color: Colors.white, fontSize: 20),
                  ),
                ],
              ),
            ),
            _buildDrawerItem(Icons.people, "Étudiants"),
            _buildDrawerItem(Icons.attach_money, "Finances"),
            _buildDrawerItem(Icons.calendar_today, "Emplois du temps"),
            _buildDrawerItem(Icons.school, "Formations payantes"),
            _buildDrawerItem(Icons.work, "Employés"),
            _buildDrawerItem(Icons.directions_bus, "Transport"),
            _buildDrawerItem(Icons.notifications, "Notifications"),
          ],
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Cartes avec infos principales
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildInfoCard("Élèves", "1200", Colors.blue),
                _buildInfoCard("Finances", "32 400 €", Colors.green),
                _buildInfoCard("Cours", "85", Colors.orange),
              ],
            ),
            SizedBox(height: 20),

            Text("Dernières activités",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),

            SizedBox(height: 10),

            Expanded(
              child: ListView(
                children: [
                  _buildActivity("Nouvelle facture générée", "Aujourd’hui 14:32"),
                  _buildActivity("Abonnement payé", "Hier 17:45"),
                  _buildActivity("Nouvelle inscription", "Hier 13:20"),
                  _buildActivity("Cours ajouté", "Lundi 10:15"),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  /// 🔹 Widget pour les éléments du menu latéral
  Widget _buildDrawerItem(IconData icon, String title) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      onTap: () {
        // ⚡ Ici tu ajouteras la navigation vers les autres pages
        // Exemple : Navigator.push(context, MaterialPageRoute(builder: (_) => StudentsPage()));
      },
    );
  }

  /// 🔹 Widget pour une carte d’info
  Widget _buildInfoCard(String title, String value, Color color) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      elevation: 3,
      child: Container(
        width: 100,
        padding: EdgeInsets.all(12),
        child: Column(
          children: [
            Text(title, style: TextStyle(fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            Text(
              value,
              style: TextStyle(fontSize: 16, color: color, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }

  /// 🔹 Widget pour une activité
  Widget _buildActivity(String title, String time) {
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      child: ListTile(
        leading: Icon(Icons.check_circle_outline, color: Colors.green),
        title: Text(title),
        trailing: Text(time, style: TextStyle(color: Colors.grey)),
      ),
    );
  }
}
