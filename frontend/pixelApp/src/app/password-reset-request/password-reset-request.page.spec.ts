import { ComponentFixture, TestBed } from '@angular/core/testing';
import { PasswordResetRequestPage } from './password-reset-request.page';

describe('PasswordResetRequestPage', () => {
  let component: PasswordResetRequestPage;
  let fixture: ComponentFixture<PasswordResetRequestPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(PasswordResetRequestPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
