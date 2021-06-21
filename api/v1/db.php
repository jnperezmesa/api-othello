<?php
//----------------------------------------------
// Recursos compartidos
//----------------------------------------------
define("URL_RAIZ", $_SERVER['DOCUMENT_ROOT']);

//===============================================
// Base de datos
//===============================================
/**
 * Función que conecta con la base de datos
 * @return object
 */
function getPDO(): object
{
    // Indicamos la ubicación de la base de datos
    $hostDB = URL_RAIZ . '/othello.sqlite';
    // Conecta con base de datos
    $hostPDO = "sqlite:$hostDB";
    // Devuelve la conexion
    return new PDO($hostPDO);
}
