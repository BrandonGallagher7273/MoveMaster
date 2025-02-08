using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class EnterCode : MonoBehaviour
{
    public TMP_InputField inputField; // Assign in Inspector
    public GameObject panel; // Reference to the panel
    private string code; // Stores user input
    private CanvasGroup canvasGroup; // Handles UI blocking

    void Start()
    {
        panel = GameObject.Find("PromptPanel");
        if (panel != null)
        {
            canvasGroup = panel.GetComponent<CanvasGroup>();
            panel.SetActive(false); // Ensure the panel starts hidden
        }
    }

    public void SubmitInput()
    {
        if (inputField != null)
        {
            code = inputField.text; // Store user input
            Debug.Log("User entered: " + code);
            HideUI();
        }
        else
        {
            Debug.LogError("InputField not assigned! Ensure it's set in the Inspector.");
        }
    }

    public void ShowUI()
    {
        if (panel != null)
        {
            panel.SetActive(true);
            if (canvasGroup != null)
            {
                canvasGroup.blocksRaycasts = true; // Prevent game interactions
                canvasGroup.interactable = true;
            }
        }
    }

    public void HideUI()
    {
        if (panel != null)
        {
            panel.SetActive(false);
            if (canvasGroup != null)
            {
                canvasGroup.blocksRaycasts = false; // Allow game interactions again
                canvasGroup.interactable = false;
            }
        }
    }
}
