# flask-rest-api-jwt
Una app sencilla que usa flask, postgresql, jwt y swagger(flasgger).  

Se debe tener en cuenta que para este caso la autorización, es decir el token Se debe agregar en el endpoint de getPrescriptionById de la siguiente anteponiendo la palabra bearer y luego el token generado, por ejemplo:  

Bearer 20eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ