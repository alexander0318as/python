<!DOCTYPE html>
<html lang="es">

<head>
<meta charset="UTF-8">
<title>Dashboard Jugador</title>

<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

/* Fondo del estadio */

body{
background-image: url("estadio.jpg");
background-size: cover;
background-position: center;
background-attachment: fixed;
}

/* capa oscura */

.overlay{
background: rgba(0,0,0,0.75);
min-height:100vh;
}

</style>

</head>

<body>

<div class="overlay">

<!-- NAVBAR -->

<nav class="bg-black/60 backdrop-blur-md">
<div class="max-w-7xl mx-auto px-6 py-4 flex justify-between">

<h1 class="text-2xl font-bold text-green-400">
⚽ Futbol Pro System
</h1>

<div class="space-x-6 text-white">
<a href="#" class="hover:text-green-400">Inicio</a>
<a href="#" class="hover:text-green-400">Partidos</a>
<a href="#" class="hover:text-green-400">Estadísticas</a>
<a href="#" class="hover:text-green-400">Equipo</a>
</div>

</div>
</nav>


<!-- PERFIL DEL JUGADOR -->

<section class="max-w-7xl mx-auto mt-10 px-6">

<div class="bg-black/60 backdrop-blur-md p-6 rounded-xl flex items-center gap-6">

<img src="" class="rounded-full w-24 h-24">

<div>

<h2 class="text-2xl font-bold text-white">
Alexander Acevedo
</h2>

<p class="text-gray-300">
Delantero • Equipo A
</p>

<div class="flex gap-6 mt-3 text-sm text-gray-300">

<span>⚽ 0 Goles</span>
<span>🎯 0 Asistencias</span>
<span>🏃 0 Partidos</span>

</div>

</div>

</div>

</section>


<!-- PROXIMOS PARTIDOS -->

<section class="max-w-7xl mx-auto mt-10 px-6">

<h3 class="text-2xl font-semibold mb-6 text-green-400">
📅 Próximos Partidos
</h3>

<div class="grid md:grid-cols-3 gap-6">

<div class="bg-black/60 backdrop-blur-md p-6 rounded-xl shadow-xl">
<p class="text-gray-300">12 Abril</p>
<h4 class="text-xl font-bold mt-2 text-white">Equipo A vs Equipo B</h4>
<p class="text-gray-400 mt-2">Estadio Central</p>
</div>

<div class="bg-black/60 backdrop-blur-md p-6 rounded-xl shadow-xl">
<p class="text-gray-300">18 Abril</p>
<h4 class="text-xl font-bold mt-2 text-white">Equipo A vs Tigres</h4>
<p class="text-gray-400 mt-2">Cancha Norte</p>
</div>

<div class="bg-black/60 backdrop-blur-md p-6 rounded-xl shadow-xl">
<p class="text-gray-300">25 Abril</p>
<h4 class="text-xl font-bold mt-2 text-white">Equipo A vs Halcones</h4>
<p class="text-gray-400 mt-2">Estadio Sur</p>
</div>

</div>

</section>


<!-- ESTADISTICAS DEL EQUIPO -->

<section class="max-w-7xl mx-auto mt-14 px-6">

<h3 class="text-2xl font-semibold mb-6 text-green-400">
📊 Estadísticas del Equipo
</h3>

<div class="overflow-x-auto">

<table class="w-full text-left bg-black/60 backdrop-blur-md rounded-xl overflow-hidden text-white">

<thead class="bg-green-600">

<tr>
<th class="p-4">Jugador</th>
<th class="p-4">Goles</th>
<th class="p-4">Asistencias</th>
<th class="p-4">Partidos</th>
</tr>

</thead>

<tbody>

<tr class="border-t border-gray-700 hover:bg-black/40">
<td class="p-4">Juan Pérez</td>
<td class="p-4">8</td>
<td class="p-4">5</td>
<td class="p-4">12</td>
</tr>

<tr class="border-t border-gray-700 hover:bg-black/40">
<td class="p-4">Carlos Gómez</td>
<td class="p-4">6</td>
<td class="p-4">7</td>
<td class="p-4">12</td>
</tr>

<tr class="border-t border-gray-700 hover:bg-black/40">
<td class="p-4">Luis Rodríguez</td>
<td class="p-4">4</td>
<td class="p-4">3</td>
<td class="p-4">10</td>
</tr>

</tbody>

</table>

</div>

</section>


<!-- RENDIMIENTO DEL EQUIPO -->

<section class="max-w-7xl mx-auto mt-14 px-6">

<h3 class="text-2xl font-semibold mb-6 text-green-400">
🏆 Rendimiento del Equipo
</h3>

<div class="grid md:grid-cols-4 gap-6">

<div class="bg-black/60 backdrop-blur-md p-6 rounded-xl text-center">
<p class="text-gray-300">Ganados</p>
<h4 class="text-3xl font-bold text-green-400 mt-2">9</h4>
</div>

<div class="bg-black/60 backdrop-blur-md p-6 rounded-xl text-center">
<p class="text-gray-300">Perdidos</p>
<h4 class="text-3xl font-bold text-red-400 mt-2">3</h4>
</div>

<div class="bg-black/60 backdrop-blur-md p-6 rounded-xl text-center">
<p class="text-gray-300">Goles a Favor</p>
<h4 class="text-3xl font-bold text-blue-400 mt-2">24</h4>
</div>

<div class="bg-black/60 backdrop-blur-md p-6 rounded-xl text-center">
<p class="text-gray-300">Goles en Contra</p>
<h4 class="text-3xl font-bold text-yellow-400 mt-2">10</h4>
</div>

</div>

</section>


<!-- GRAFICA -->

<section class="max-w-4xl mx-auto mt-14 px-6">

<h3 class="text-2xl font-semibold mb-6 text-green-400 text-center">
📈 Rendimiento del Equipo
</h3>

<div class="bg-black/60 backdrop-blur-md p-6 rounded-xl">

<canvas id="grafica"></canvas>

</div>

</section>


<footer class="mt-16 text-center text-gray-400 pb-6">
© By System Pro Futbol
</footer>

</div>


<script>

const ctx = document.getElementById('grafica');

new Chart(ctx, {
type: 'bar',
data: {
labels: ['Ganados','Empates','Perdidos'],
datasets: [{
label: 'Partidos',
data: [9,2,3],
backgroundColor:[
'#22c55e',
'#facc15',
'#ef4444'
]
}]
},
options:{
plugins:{
legend:{display:false}
}
}
});

</script>

</body>
</html>