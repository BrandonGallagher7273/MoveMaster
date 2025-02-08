using UnityEngine;

public class PromptPlayer : MonoBehaviour
{
    public GameObject panel;

    void Start() 
    {
        panel = GameObject.Find("PromptPanel");

        if (panel == null)
        {
            Debug.LogError("PromptPanel not found! Ensure it's in the scene.");
        }
    }

    public void ShowPrompt()  
    {
        if (panel != null)
        {
            panel.SetActive(true); // Show the UI Panel
        }
    }
}
