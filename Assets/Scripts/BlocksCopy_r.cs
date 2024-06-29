using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlocksCopy_4 : MonoBehaviour
{

    public GameObject prefab;
    public int blocks = 27;

    void Start()
    {
        int flag = 0;
        int count = -1;
        for (int i = 0; i <= blocks/3; i++) {
            for (int p = 0; p < 3; p++) {
                GameObject clone = Instantiate(prefab);
                clone.transform.position = new Vector3(50.75f,.91f*count+.9f,49.25f+p*0.75f);
            }
            count++;
        }
        

    }
}
