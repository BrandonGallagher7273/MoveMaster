using UnityEngine;

public class ShowUI : MonoBehaviour
{
    public GameObject panel;

    void Start()
    {

        if (panel == null)
        {
            Debug.LogError("PromptPanel not found! Check if it's in the scene.");
        }
        else
        {
            panel.SetActive(false); // Ensure the panel starts hidden
        }
    }

    void OnMouseDown()
    {
        if (panel != null)
        {
            PromptPlayer show = panel.GetComponent<PromptPlayer>();
            if (show != null)
            {
                Debug.Log("here!\n");
                show.ShowPrompt();
            }
            else
            {
                Debug.LogError("PromptPlayer script not found on PromptPanel!");
            }
        }
    }
}
