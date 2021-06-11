<?php
use PHPUnit\Framework\TestCase;

require_once('crearUsuario.php');


class CrearUsuarioTest extends TestCase
{

    public function testCrearId(): void
    {
        $id = crearId(7);
        $this->assertSame(strlen($id), 7, "$id no tiene los suficientes caracteres");
    }

}
