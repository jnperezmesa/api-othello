<?php
//----------------------------------------------------------------------------------------------------------------------------------
// Recursos compartidos
//----------------------------------------------------------------------------------------------------------------------------------
require_once('recursos.php');

//=================================================================================================================================
// Crear nuevo usuario
//=================================================================================================================================

//----------------------------------------------------------------------------------------------------------------------------------
// Variables
//----------------------------------------------------------------------------------------------------------------------------------
$accionCrearUsuario = isset($_REQUEST['nuevo_jugador']);


//----------------------------------------------------------------------------------------------------------------------------------
// Funciones
//----------------------------------------------------------------------------------------------------------------------------------
/**
 * Función que comprueba si existe un usuario
 * @param object $miPDO
 * @param string $id
 * @return bool
 */
function comprobarIdUsuario(object $miPDO, string $id): bool
{
    $miInsert = $miPDO->prepare("select count(id_jugador) AS existe from jugadores WHERE id_jugador = :id_jugador;");
    $miInsert->execute([
        'id_jugador' => $id,
    ]);
    $resultado = $miInsert->fech();
    return $resultado;
}

/**
 * Función que guarda el usuario en la base de datos
 * @param object $miPDO
 * @param string $id
 * @return bool
 */
function guardarIdUsuario(object $miPDO, string $id): bool
{
    $valido = $_SERVER['REQUEST_METHOD'] == 'POST';
    if ($valido) {
        $miInsert = $miPDO->prepare("INSERT INTO jugadores (id_jugador, fecha_creacion) VALUES (:id_jugador, datetime('now'));");
        $miInsert->execute([
            'id_jugador' => $id,
        ]);
    }
    return $valido;
}

/**
 * Función que crea el usuario y devuelve el id
 * @param object $miPDO
 */
function crearUsuario(object $miPDO): string
{
    $id = crearId(7);
    if (comprobarIdUsuario($miPDO, $id)) {
        crearUsuario($miPDO);
    } else {
        guardarIdUsuario($miPDO, $id);
        return $id;
    }
}

//----------------------------------------------------------------------------------------------------------------------------------
// Inicio
//----------------------------------------------------------------------------------------------------------------------------------
if ($accionCrearUsuario) {
    $miPDO = getPDO();
    $id_jugador = crearUsuario($miPDO);
}