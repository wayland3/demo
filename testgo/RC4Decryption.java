import javax.crypto.*;
import java.nio.charset.StandardCharsets;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.net.URLDecoder;
import java.util.Base64;

public final class RC4Decryption {

    public static String decrypt(String encodedMessage, String encryptionKey)
            throws BadPaddingException, IllegalBlockSizeException,
            NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException {
        SecureRandom secureRandom = SecureRandom.getInstance("SHA1PRNG");
        secureRandom.setSeed(encryptionKey.getBytes());
        KeyGenerator keyGenerator = KeyGenerator.getInstance("RC4");
        keyGenerator.init(secureRandom);
        SecretKey key = keyGenerator.generateKey();
        Cipher cipher = Cipher.getInstance("RC4");
        cipher.init(Cipher.DECRYPT_MODE, key);

        System.out.println("new key: " + key);
        byte[] encryptedMessageBytes = Base64.getDecoder().decode(encodedMessage);

        byte[] decryptedMessageBytes = cipher.doFinal(encryptedMessageBytes);
        return new String(decryptedMessageBytes, StandardCharsets.UTF_8);
    }


    public static void main(String[] args) {
        String encodedMessage ="0OgzgpADo4SOia%2FpjpolWQJS7Oqr9VksSB5Dz2jG9ToemmBZnmlw3fVzaBvuWaGWYdFK22zVyKmftuLB6Mk%3D";
        try {
            encodedMessage = URLDecoder.decode(encodedMessage, "UTF-8");
        } catch (Exception e) {
            System.err.println("Failed to decode URL: " + e.getMessage());
            return;
        }

        System.out.println("url decode: " + encodedMessage);

        String encryptionKey = "$Yrk%*af"; // Replace with your RC4 encryption key

        try {
            String decryptedMessage = RC4Decryption.decrypt(encodedMessage, encryptionKey);
            System.out.println("Decrypted message: " + decryptedMessage);
        } catch (NoSuchAlgorithmException | NoSuchPaddingException | InvalidKeyException
                 | IllegalBlockSizeException | BadPaddingException e) {
            System.err.println("Decryption failed: " + e.getMessage());
        }
    }
}
