<?php

function getPDO(): object
{
    // Indicamos la ubicación de la base de datos
    $hostDB = '../othello.sqlite';
    // Conecta con base de datos
    $hostPDO = "sqlite:$hostDB";
    // Devuelve la conexion
    return new PDO($hostPDO);
}
