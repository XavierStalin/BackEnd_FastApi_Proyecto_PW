
import sys
import smtplib
from config import get_settings

def test_smtp():
    print("--- Iniciando prueba de conexión SMTP ---")
    
    try:
        settings = get_settings()
        print(f"Configuración cargada:")
        print(f"  Servidor: {settings.MAIL_SERVER}")
        print(f"  Puerto: {settings.MAIL_PORT}")
        print(f"  Usuario: {settings.MAIL_USERNAME}")
        print(f"  From: {settings.MAIL_FROM}")
        # No imprimimos la contraseña por seguridad
        
        print(f"\n[1/3] Intentando conectar a {settings.MAIL_SERVER}:{settings.MAIL_PORT}...")
        try:
            server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT, timeout=30)
            server.set_debuglevel(1)  # Ver logs detallados del protocolo
            print("  [OK] Conexión TCP establecida.")
        except Exception as e:
            print(f"  [ERROR] Falló la conexión TCP: {e}")
            return

        print("\n[2/3] Intentando STARTTLS...")
        try:
            server.starttls()
            print("  [OK] STARTTLS exitoso.")
        except Exception as e:
            print(f"  [ERROR] Falló STARTTLS: {e}")
            server.quit()
            return

        print("\n[3/3] Intentando autenticación (Login)...")
        try:
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            print("  [OK] Login exitoso.")
        except smtplib.SMTPAuthenticationError as e:
            print(f"  [ERROR] Falló la autenticación: {e}")
            print("     -> Verifique que 'Acceso de aplicaciones menos seguras' esté activado o use una 'Contraseña de aplicación'.")
        except Exception as e:
            print(f"  [ERROR] Error inesperado en login: {e}")
        finally:
            server.quit()
            
    except Exception as e:
        print(f"[ERROR] Error general en la prueba: {e}")

if __name__ == "__main__":
    test_smtp()
