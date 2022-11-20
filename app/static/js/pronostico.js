$(document).ready(function () {

})

const cargarPartido = async (id, csrf) => {
    const params = { id: id }
    await fetch(`/partido`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-TOKEN": csrf,
        },
        body: JSON.stringify(params) 
    }).then((response) => response.text())
    .then((data) => {
        const response = JSON.parse(data)
        if(response.success){
            let datos = response.data
            let pronos = response.pronostico
            console.log(datos.estado)
            document.getElementById('idpartido').value = datos.idPartido
            document.getElementById('idEquipo1').value = datos.idEq1
            document.getElementById('idEquipo2').value = datos.idEq2
            document.getElementById('lbl_eq1').innerHTML = datos.nomEquipo1
            document.getElementById('lbl_eq2').innerHTML = datos.nomEquipo2
            if(pronos){
                document.getElementById('txt_resulEq1').value = pronos.goles_equipo1
                document.getElementById('txt_resulEq2').value = pronos.goles_equipo2            
            }else{
                document.getElementById('txt_resulEq1').value = ''
                document.getElementById('txt_resulEq2').value = ''     
            }
            /* Swal.fire({
                title:'¡ Proceso exitoso !',
                html: response.msg,
                type: 'success',
                showConfirmButton: true,
                confirmButtonColor: '#3085d6',
            }).then((result) => {
               
            }) */
        }else{
          Swal.fire({
              title: 'Ocurrio el siguiente problema: ',
              html: response.msg,
              type: 'error',
              showConfirmButton: true,
              confirmButtonColor: '#3085d6',
          })
        }
    })
}