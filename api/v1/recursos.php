<?php
//==============================================
// Recursos compartidos
//==============================================

//----------------------------------------------
// Constantes
//----------------------------------------------
define("URL_RAIZ", $_SERVER['DOCUMENT_ROOT']);

//----------------------------------------------
// Variables
//----------------------------------------------

//----------------------------------------------
// Funciones
//----------------------------------------------
/**
 * Función que crea identificadores alfanumericos
 * @param int $caracteres
 * @return string
 */
function crearId(int $caracteres): string
{
    $palabras = range('a', 'z');
    $palabra_array = [];
    foreach (range(1, $caracteres) as $item) {
        $num = rand(0, 10);
        if ($num <= 6) {
            $palabra_array[] = $palabras[rand(0, count($palabras))];
        } else {
            $palabra_array[] = rand(0, 9);
        }
    }
    $id = str_replace(',', '',implode(',',$palabra_array));
    return $id;
}

// Base de datos
require_once(URL_RAIZ . 'db.php');
