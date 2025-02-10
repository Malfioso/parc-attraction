import { Component, Input, OnInit } from '@angular/core';
import { CritiqueService } from '../Service/comments.service';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';
import { Critique } from '../Interface/comments.interface';
import { MatCardModule } from '@angular/material/card';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-critiques',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSnackBarModule, // Add this if it's missing
  ],
  templateUrl: './comments.component.html',
  styleUrl: './comments.component.scss',
})
export class CommentsComponent implements OnInit {
  attractionId?: number;

  public critiques: Observable<Critique[]>;
  public newCritique: Critique = {
    critique_id: 0,
    note: 0,
    commentaire: '',
    attraction_id: 0,
    users_id: 1, // This should come from your auth service
  };

  constructor(
    public critiqueService: CritiqueService,
    private snackBar: MatSnackBar,
    private route: ActivatedRoute
  ) {
    this.critiques = this.critiqueService.getAllCritiques();
  }

  ngOnInit() {
    this.route.params.subscribe((params) => {
      if (params['attractionId']) {
        this.attractionId = +params['attractionId'];
        this.critiques = this.critiqueService.getCritiquesByAttractionId(
          this.attractionId
        );
        this.newCritique.attraction_id = this.attractionId;
      }
    });
  }

  submitCritique() {
    // Validate data before sending
    if (
      !this.newCritique.note ||
      !this.newCritique.commentaire ||
      !this.attractionId
    ) {
      this.snackBar.open('Please fill in all required fields', 'Close', {
        duration: 3000,
      });
      return;
    }

    // Ensure the attraction_id is set
    this.newCritique.attraction_id = this.attractionId;

    // Ensure user_id is set (you might want to get this from your auth service)
    this.newCritique.users_id = 1; // Replace with actual user ID from auth

    console.log('Submitting critique:', this.newCritique);

    this.critiqueService.postCritique(this.newCritique).subscribe({
      next: (response) => {
        console.log('Success response:', response);
        this.snackBar.open('Comment added successfully!', 'Close', {
          duration: 3000,
        });

        // Reset the form
        this.newCritique = {
          critique_id: 0,
          note: 0,
          commentaire: '',
          attraction_id: this.attractionId || 0,
          users_id: 1, // Replace with actual user ID
        };

        // Refresh critiques list
        if (this.attractionId) {
          this.critiques = this.critiqueService.getCritiquesByAttractionId(
            this.attractionId
          );
        } else {
          this.critiques = this.critiqueService.getAllCritiques();
        }
      },
      error: (error) => {
        console.error('Error details:', error);
        this.snackBar.open(
          `Error adding comment: ${error.status} ${error.message}`,
          'Close',
          {
            duration: 3000,
          }
        );
      },
    });
  }
}
