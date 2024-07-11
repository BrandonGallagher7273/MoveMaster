using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlocksCopy : MonoBehaviour
{
    public GameObject prefab;
    public int blocks = 27;
    public int a = -1;
    public int b = -1;
    int tag_i = 28;
    string tag_s;

    void Start()
    {
        if (a > 8) {
            a = -1;
        }
        if (b > 2) {
            b = -1;
        }
        int count = 0;
        for (int i = 0; i < blocks/3; i++) {
            for (int p = 0; p < 3; p++) {
                if (i != a || p != b) {
                    tag_s = tag_i.ToString();
                    GameObject clone = Instantiate(prefab);
                    clone.tag = "Selectable";
                    clone.transform.position = new Vector3(50+p*0.75f,.92f*count,50);
                    tag_i++;
                }
            }
            count++;
        }

    }
    /*
    void Update() {
        if (Input.GetMouseButton (0)) {
            Destroy(GameObject.FindGameObjectWithTag(tag_s));
        }
    }
    */

 }


